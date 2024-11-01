// Cell types
export interface EmptyCell {
    type: "EmptyCell";
}

export interface ElectronHead {
    type: "ElectronHead";
}

export interface ElectronTail {
    type: "ElectronTail";
}

export interface Conductor {
    type: "Conductor";
}

export type CellUnion = EmptyCell | ElectronHead | ElectronTail | Conductor;

// Component types
export interface ClockGenerator {
    type: "ClockGenerator";
    period: number;
    start_step: number;
    stop_step: number | null;
    counter: number;
}

export enum DiodeDirection {
    LEFT = "LEFT",
    RIGHT = "RIGHT"
}

export interface Diode {
    type: "Diode";
    direction: DiodeDirection;
}

export enum ElectronFlow {
    LEFT_TO_RIGHT = "LEFT_TO_RIGHT",
    RIGHT_TO_LEFT = "RIGHT_TO_LEFT",
    UP_TO_DOWN = "UP_TO_DOWN",
    DOWN_TO_UP = "DOWN_TO_UP",
    NONE = "NONE"
}

export interface Detector {
    type: "Detector";
    last_detection: number;
    period: number;
    last_flow: ElectronFlow;
}

export type ComponentUnion = ClockGenerator | Diode | Detector;

// Grid types
export interface GridState {
    cell_grid: CellUnion[][];
    component_grid: (ComponentUnion | null)[][];
    step: number;
}

// Utility types for configuration
export interface ClockConfig {
    type: "ClockConfig";
    x: number;
    y: number;
    period: number;
    start_step: number;
    stop_step?: number;
}

export interface DiodeConfig {
    type: "DiodeConfig";
    x: number;
    y: number;
    direction: DiodeDirection;
}

export type ComponentConfigType = ClockConfig | DiodeConfig;
