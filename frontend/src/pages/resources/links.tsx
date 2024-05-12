import React from "react";
import QueryGuard from "../../components/query-guard";
import QueryFallback from "../../components/QueryFallback";

const Links = () => {
  return <div>Hey</div>;
};

const LinksWithGuard = () => {
  const query = React.useCallback(async (params: undefined) => {
    return {};
  }, []);
  return (
    <QueryGuard
      render={Links}
      props={{}}
      query={query}
      args={undefined}
      fallback={QueryFallback()}
    />
  );
};

export default LinksWithGuard;
