import React from 'react';

interface TestComponentProps {
  title: string;
  description?: string;
}

export function TestComponent({ title, description }: TestComponentProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 space-y-2">
      {/* This should trigger design violations */}
      <h2 className="text-xl font-bold text-gray-900">{title}</h2>
      {description && (
        <p className="text-sm font-normal text-gray-600">{description}</p>
      )}
      {/* Small touch target - should warn */}
      <button className="h-10 px-3 bg-blue-500 text-white rounded-lg">
        Click me
      </button>
    </div>
  );
}
