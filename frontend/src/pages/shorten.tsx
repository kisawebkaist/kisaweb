import FaqAPI, { CategoryT, FaqT } from "../API/faq";
import FaqCategory from "../components/faq/FaqCategory";
import FaqHeader from "../components/faq/FaqHeader";
import FaqQuestion from "../components/faq/FaqQuestion";
import FaqSearch from "../components/faq/FaqSearch";
import QueryGuard from "../components/query-guard";
import React, { useEffect } from "react";
import { Typography, Stack } from "@mui/material";
import { Container, Box } from "@mui/system";
import Lister from "../components/lister";
import QueryFallback from "../components/QueryFallback";
import { redirect, useParams } from "react-router-dom";
import UrlShortener from "../API/url-shortener";

type ShortenP = {
  link?: string;
};

const Shorten = ({ link }: ShortenP) => {
  useEffect(() => {
    let path = "/";
    if (link) {
      path = link;
    }
    window.location.href = path;
  }, []);
  return <div></div>;
};

const ShortenWithGuard = () => {
  const params = useParams();

  const query = React.useCallback<(params: undefined) => Promise<ShortenP>>(
    async (_) => {
      const slug = params.slug;
      if (!slug) return {};
      const link = await UrlShortener.expandUrl(slug);
      return { link };
    },
    []
  );
  return (
    <QueryGuard
      render={Shorten}
      props={{}}
      query={query}
      args={undefined}
      fallback={QueryFallback()}
    />
  );
};

export default ShortenWithGuard;
