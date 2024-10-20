import React, { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'danger';
}

export const Button: React.FC<ButtonProps> = ({
    children,
    className = '',
    variant = 'primary',
    ...props
}) => {
    const baseStyles = 'px-4 py-2 rounded font-semibold text-sm transition-colors duration-200';
    const variantStyles = {
        primary: 'bg-nord10 text-nord6 hover:bg-nord9 disabled:bg-nord3',
        danger: 'bg-nord11 text-nord6 hover:bg-nord12 disabled:bg-nord3',
    };

    return (
        <button
            className={`${baseStyles} ${variantStyles[variant]} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
};
