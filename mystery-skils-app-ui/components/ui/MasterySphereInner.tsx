/**
 * MasterySphereInner.tsx
 *
 * Stub component - 3D visualization disabled for Flash UI
 */

'use client'

interface MasteryLevel {
  skill: string
  progress: number // 0-100
}

interface Props {
  masteryLevels: MasteryLevel[]
}

/**
 * 3D Mastery Sphere (Disabled)
 */
export function MasterySphere({ masteryLevels }: Props) {
  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="text-gray-500 text-sm">3D Sphere Disabled</div>
    </div>
  )
}
