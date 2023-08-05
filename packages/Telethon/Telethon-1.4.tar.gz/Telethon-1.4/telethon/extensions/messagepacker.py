import asyncio
import collections
import io
import logging
import struct

from ..tl import TLRequest
from ..tl.core.messagecontainer import MessageContainer
from ..tl.core.tlmessage import TLMessage

__log__ = logging.getLogger(__name__)


class MessagePacker:
    """
    This class packs `RequestState` as outgoing `TLMessages`.

    The purpose of this class is to support putting N `RequestState` into a
    queue, and then awaiting for "packed" `TLMessage` in the other end. The
    simplest case would be ``State -> TLMessage`` (1-to-1 relationship) but
    for efficiency purposes it's ``States -> Container`` (N-to-1).

    This addresses several needs: outgoing messages will be smaller, so the
    encryption and network overhead also is smaller. It's also a central
    point where outgoing requests are put, and where ready-messages are get.
    """
    def __init__(self, state, loop):
        self._state = state
        self._loop = loop
        self._deque = collections.deque()
        self._ready = asyncio.Event(loop=loop)

    def append(self, state):
        self._deque.append(state)
        self._ready.set()

    def extend(self, states):
        self._deque.extend(states)
        self._ready.set()

    async def get(self):
        """
        Returns (batch, data) if one or more items could be retrieved.

        If the cancellation occurs or only invalid items were in the
        queue, (None, None) will be returned instead.
        """
        if not self._deque:
            self._ready.clear()
            await self._ready.wait()

        buffer = io.BytesIO()
        batch = []
        size = 0

        # Fill a new batch to return while the size is small enough
        while self._deque:
            state = self._deque.popleft()
            size += len(state.data) + TLMessage.SIZE_OVERHEAD

            if size <= MessageContainer.MAXIMUM_SIZE:
                state.msg_id = self._state.write_data_as_message(
                    buffer, state.data, isinstance(state.request, TLRequest),
                    after_id=state.after.msg_id if state.after else None
                )
                batch.append(state)
                __log__.debug('Assigned msg_id = %d to %s (%x)',
                              state.msg_id, state.request.__class__.__name__,
                              id(state.request))
                continue

            # Put the item back since it can't be sent in this batch
            self._deque.appendleft(state)
            if batch:
                break

            # If a single message exceeds the maximum size, then the
            # message payload cannot be sent. Telegram would forcibly
            # close the connection; message would never be confirmed.
            state.future.set_exception(
                ValueError('Request payload is too big'))

            size = 0
            continue

        if not batch:
            return None, None

        if len(batch) > 1:
            # Inlined code to pack several messages into a container
            data = struct.pack(
                '<Ii', MessageContainer.CONSTRUCTOR_ID, len(batch)
            ) + buffer.getvalue()
            buffer = io.BytesIO()
            container_id = self._state.write_data_as_message(
                buffer, data, content_related=False
            )
            for s in batch:
                s.container_id = container_id

        data = buffer.getvalue()
        return batch, data
