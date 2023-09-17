import React from "react"
import { RenderElementTypeT } from "./common"

type QueryGuardChildP<QueryResult, Additional> = QueryResult & Additional
type QueryGuardP<
  Query extends Record<string, any>,
  Additional extends Record<string, any>,
  Args
> = {
  render : RenderElementTypeT<QueryGuardChildP<Query, Additional>>
  props : Additional
  query : (params : Args) => Promise<Query>
  args : Args,
  fallback?: React.ReactNode
}

/**
 * Query Guard performs a query and guards the component below it guaranteeing
 * that the component below it will definitely get the query result.
 */
const QueryGuard =
<Q extends Record<string, any>, A extends Record<string, any>, Args>(
  {
    props, query, render : Component, fallback = null, args
  } : QueryGuardP<Q, A, Args>
) => {
  const [queryData, setQueryData] = React.useState<null | Q>(null)
  React.useEffect(() => {
    query(args)
    .then(setQueryData)
    .catch(console.error)
  }, [ args, query])
  const element = React.useMemo<React.ReactNode>(
    () => {
      if (queryData === null){
        return fallback
      }
      else{
        const renderProps = {
          ...props, ...queryData
        } as React.PropsWithRef<QueryGuardChildP<Q, A>> & QueryGuardChildP<Q, A>
        return (
          <Component {...renderProps} />
        )
      }
    }, [Component, props, queryData]
  )
  return (
    <React.Fragment>
      {element}
    </React.Fragment>
  )
}

export default QueryGuard
