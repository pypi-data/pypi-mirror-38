import { Channel } from './channel';

export interface Event {
    event: string;
    block_number: number;
    timestamp?: Date;
    token_address?: string;
    channel_manager_address?: string;
    settle_timeout?: number;
    netting_channel?: string;
    participant1?: string;
    participant2?: string;
    participant?: string;
    balance?: number;
    identifier?: number;
    data?: string;
}

export interface EventsParam {
    channel?: ChannelInformation;
    token?: string;
    activity?: boolean;
}

export interface ChannelInformation {
    token_address: string;
    partner_address: string;
}
