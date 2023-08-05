from raiden.exceptions import RaidenUnrecoverableError
from raiden.transfer import node, views
from raiden.transfer.state import NettingChannelState
from raiden.utils import pex, typing

from .wal import restore_to_state_change


def channel_state_until_state_change(
        raiden: 'RaidenService',
        payment_network_identifier: typing.PaymentNetworkID,
        token_address: typing.TokenAddress,
        channel_identifier: typing.ChannelID,
        state_change_identifier: int,
) -> typing.Optional[NettingChannelState]:
    """ Go through WAL state changes until a certain balance hash is found. """
    # Restore state from the latest snapshot
    wal = restore_to_state_change(
        node.state_transition,
        raiden.wal.storage,
        state_change_identifier,
    )

    channel_state = views.get_channelstate_by_id(
        chain_state=wal.state_manager.current_state,
        payment_network_id=payment_network_identifier,
        token_address=token_address,
        channel_id=channel_identifier,
    )

    if not channel_state:
        raise RaidenUnrecoverableError(
            f"Channel was not found before state_change {pex(state_change_identifier)}",
        )

    return channel_state
