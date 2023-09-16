import React from "react"
export type RenderElementTypeT<T> =
  React.ComponentType<T> | React.LazyExoticComponent<React.ComponentType<T>>

