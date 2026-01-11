import React from 'react'
import { clsx } from 'clsx'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hover?: boolean
}

const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  padding = 'md',
  hover = false,
  className,
  ...props
}) => {
  const baseStyles = 'rounded-lg'
  
  const variants = {
    default: 'bg-white border border-gray-200',
    elevated: 'bg-white shadow-md border border-gray-100',
    outlined: 'border-2 border-gray-300',
  }
  
  const paddings = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }
  
  return (
    <div
      className={clsx(
        baseStyles,
        variants[variant],
        paddings[padding],
        hover && 'hover:shadow-lg transition-shadow duration-200',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export default Card
