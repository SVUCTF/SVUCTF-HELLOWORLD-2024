import React from 'react';
import { ComponentUnion } from '../../types/wireworld';

interface TooltipProps {
    component: ComponentUnion | null;
}

const getComponentTooltip = (component: ComponentUnion): string => {
    switch (component.type) {
        case 'ClockGenerator':
            return `Clock Generator\nPeriod: ${component.period}\nStart Step: ${component.start_step}\nStop Step: ${component.stop_step || 'N/A'}`;
        case 'Diode':
            return `Diode\nDirection: ${component.direction}`;
        case 'Detector':
            return `Detector\nLast Detection: ${component.last_detection}\nPeriod: ${component.period}\nLast Flow: ${component.last_flow}`;
        default:
            return 'Unknown Component';
    }
};

const Tooltip: React.FC<TooltipProps> = ({ component }) => {
    if (!component) return null;

    return (
        <div className="bg-nord2 text-nord6 p-2 rounded shadow-lg whitespace-pre-line">
            {getComponentTooltip(component)}
        </div>
    );
};

export default Tooltip;
