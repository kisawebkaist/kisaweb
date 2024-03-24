import React from "react";
import QueryGuard from "../../components/query-guard";
import QueryFallback from "../../components/QueryFallback";

interface ConstitutionP {}

const Constitution = (props: ConstitutionP) => {
  return <></>;
};

const ConstitutionWithGuard = () => {
  const query = React.useCallback<
    (params: undefined) => Promise<ConstitutionP>
  >(async (params: undefined) => {
    return {};
  }, []);
  return (
    <QueryGuard
      render={Constitution}
      props={{}}
      query={query}
      args={undefined}
      fallback={QueryFallback()}
    />
  );
};

export default ConstitutionWithGuard;
