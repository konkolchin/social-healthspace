import { useState } from 'react'

export default function TestComponent() {
  console.error("TEST COMPONENT LOADED")
  
  const [count, setCount] = useState(0)

  return (
    <div className="p-4">
      <h1 className="text-2xl">Test Component</h1>
      <button 
        onClick={() => {
          console.error("Button clicked!")
          setCount(count + 1)
        }}
        className="bg-blue-500 text-white p-2 rounded"
      >
        Click me: {count}
      </button>
    </div>
  )
} 