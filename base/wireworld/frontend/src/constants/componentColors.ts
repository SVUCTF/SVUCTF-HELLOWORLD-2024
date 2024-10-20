import { ComponentUnion } from '../types/wireworld';

export const COMPONENT_COLORS: Record<ComponentUnion['type'], string> = {
    ClockGenerator: 'text-nord8',
    Diode: 'text-nord10',
    Detector: 'text-nord12'
};
