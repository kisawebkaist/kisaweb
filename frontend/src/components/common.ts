import React from "react"
export type RenderElementTypeT<Props> =
  React.ComponentType<Props> |
  React.LazyExoticComponent<React.ComponentType<Props>>

