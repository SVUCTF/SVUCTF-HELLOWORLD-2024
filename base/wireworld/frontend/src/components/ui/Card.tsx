import React from 'react';

interface CardProps {
    title: string;
    children: React.ReactNode;
    className?: string;
}

export const Card: React.FC<CardProps> = ({ title, children, className = '' }) => {
    return (
        <div className={`bg-nord2 p-4 rounded shadow ${className}`}>
            <h2 className="text-xl font-semibold mb-2 text-nord6">{title}</h2>
            {children}
        </div>
    );
};
