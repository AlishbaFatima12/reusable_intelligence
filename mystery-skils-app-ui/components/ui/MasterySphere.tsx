'use client'

import dynamic from 'next/dynamic'

const MasterySphereInner = dynamic(() => import('./MasterySphereInner').then(mod => ({ default: mod.MasterySphere })), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-full"><div className="text-cyan-400 animate-pulse">Loading 3D Visualization...</div></div>
})

export function MasterySphere(props: any) {
  return <MasterySphereInner {...props} />
}
