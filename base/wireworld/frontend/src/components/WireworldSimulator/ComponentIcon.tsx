import React from 'react';
import { Clock, ArrowRight, ArrowLeft, Activity } from 'lucide-react';
import { ComponentUnion, DiodeDirection } from '../../types/wireworld';

interface ComponentIconProps {
    component: ComponentUnion;
    size: number;
    className?: string;
}

const ComponentIcon: React.FC<ComponentIconProps> = ({ component, size, className }) => {
    switch (component.type) {
        case 'ClockGenerator':
            return <Clock size={size} className={className} />;
        case 'Diode':
            return component.direction === DiodeDirection.LEFT
                ? <ArrowLeft size={size} className={className} />
                : <ArrowRight size={size} className={className} />;
        case 'Detector':
            return <Activity size={size} className={className} />;
        default:
            return null;
    }
};

export default ComponentIcon;
