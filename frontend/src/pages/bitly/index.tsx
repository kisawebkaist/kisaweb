import React from "react";
import { useParams } from "react-router-dom";
import UrlShortener from "../../API/url-shortener";
import { Stack, Icon, Typography } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faSadCry, faSearch } from "@fortawesome/free-solid-svg-icons";

const ShortenWithGuard = () => {
  // null indicates loading failed.
  const params = useParams();
  const [url, setUrl] = React.useState<undefined | string | null>(undefined);

  React.useEffect(() => {
    if (params.slug === undefined) return;
    UrlShortener.expandUrl(params.slug)
      .then((redirectLink) => {
        setUrl(redirectLink);
        setTimeout(() => {
          if (typeof redirectLink === "string")
            window.location.href = redirectLink;
        }, 300);
      })
      .catch((err) => {
        if (err.response.status === 404) setUrl(null);
        console.error(err);
      });
  }, [params]);

  /**
   * Note to Alisher. This is probably more elegant !
   */
  // This renders before the url is loaded
  return (
    <Stack
      direction="column"
      justifyContent="center"
      alignItems="center"
      className = "-translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 absolute"
    >
      <Icon className="text-4xl mb-4" color="info">
        {url === undefined && (
          <FontAwesomeIcon icon={faSearch} className="animate-pulse" />
        )}
        {url === null && <FontAwesomeIcon icon={faSadCry} />}
        {typeof url === "string" && <FontAwesomeIcon icon={faCheck} />}
      </Icon>
      <Typography variant="h1" className="text-2xl">
        {url === null && "No links found"}
        {url === undefined && "Finding your link !"}
        {typeof url === "string" && "Showing you the cool link !"}
      </Typography>
    </Stack>
  );
};

export default ShortenWithGuard;
