import { CellUnion, ComponentUnion } from './wireworld';

export interface Meta {
    name: string;
    description: string;
    cell_descriptions: Record<string, string>;
    component_descriptions: Record<string, string>;
}

export interface Grid {
    width: number;
    height: number;
    max_steps: number;
}

export interface EditableArea {
    x: number;
    y: number;
    width: number;
    height: number;
}

export interface GridState {
    cell_grid: CellUnion[][];
    component_grid: (ComponentUnion | null)[][];
    step: number;
}

export interface ChallengeInfo {
    meta: Meta;
    grid: Grid;
    editable_area: EditableArea;
    initial_state: GridState;
}

export interface ChallengeResult {
    message: string;
    success: boolean | undefined;
    flag: string | null;
}


export interface SimulateMessage {
    type: 'simulate';
    design: CellUnion[][];
}

export interface GetInfoMessage {
    type: 'get_info';
}

export interface ResetMessage {
    type: 'reset';
}

export interface SimulationResultMessage {
    type: 'simulation_result';
    success: boolean;
    final_state: GridState;
    flag: string | null;
}

export interface WorldUpdateMessage {
    type: 'world_update';
    grid_state: GridState;
}

export interface ChallengeInfoMessage {
    type: 'challenge_info';
    meta: Meta;
    grid: Grid;
    editable_area: EditableArea;
    initial_state: GridState;
}

export interface ErrorMessage {
    type: 'error';
    message: string;
}

export type WebSocketMessageUnion = SimulateMessage | GetInfoMessage | ResetMessage;
export type WebSocketResponseUnion = SimulationResultMessage | WorldUpdateMessage | ChallengeInfoMessage | ErrorMessage;
