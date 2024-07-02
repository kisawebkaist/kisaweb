import { CategoryT, LinkT } from "../API/links";
import LinkCategory from "../components/links/LinkCategory";
import LinkHeader from "../components/links/LinkHeader";
import LinkEntity from "../components/links/LinkEntity";
import LinkSearch from "../components/links/LinkSearch";
import QueryGuard from "../components/query-guard";
import React from "react";
import { List, Stack, Typography } from "@mui/material";
import { Container, Box } from "@mui/system";
import Lister from "../components/lister";
import QueryFallback from "../components/QueryFallback";
import LinkAPI from "../API/links";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLinkSlash } from "@fortawesome/free-solid-svg-icons";

// Define the expected types for faqs and categories
type LinksP = {
  links: LinkT[];
  categories: CategoryT[];
};

const generalCategory: CategoryT = {
  id: -1,
  title_category: "All",
  title_slug: "all_general_all",
};

const Faq = ({ links, categories }: LinksP) => {
  const [searchText, setSearchText] = React.useState<string>();
  const [activeCategory, setActiveCategory] = React.useState<number>(-1);
  const [filteredLinks, setFilteredLinks] = React.useState<LinkT[]>(links);

  React.useEffect(() => {
    setFilteredLinks(
      links.filter((link: LinkT) => {
        let isAccepted = true;
        if (searchText !== undefined) {
          if (
            !(
              link.title.toLowerCase().includes(searchText.toLowerCase()) ||
              link.description.toLowerCase().includes(searchText.toLowerCase())
            )
          ) {
            isAccepted = false;
          }
        }
        if (activeCategory !== -1) {
          if (link.category !== activeCategory) {
            isAccepted = false;
          }
        }
        return isAccepted ? link : null;
      })
    );
  }, [activeCategory, searchText, links]);

  const linkContents = React.useMemo(() => {
    if (filteredLinks.length !== 0)
      return <Lister array={filteredLinks} render={LinkEntity} props={{}} />;
    return (
      <Stack className="h-80 opacity-50 gap-y-4">
        <FontAwesomeIcon icon = {faLinkSlash} className = "text-5xl"/>
        <Typography variant="body2" textAlign="center" className="text-5xl">
          No Questions Yet
        </Typography>
      </Stack>
    );
  }, [filteredLinks]);

  const isActiveCategory = (category: CategoryT) => {
    return activeCategory === category.id;
  };
  return (
    <Container maxWidth="md">
      {/* Header */}
      <LinkHeader />
      {/* Search */}
      <LinkSearch onSearch={setSearchText} />
      <Stack direction="row" justifyContent="space-between">
        {/* Categories */}
        <Box component="nav" className = "w-3/12 mr-2">
          <List>
            <Lister
              array={[generalCategory, ...categories]}
              render={LinkCategory}
              props={{
                isActiveCategory,
                setActiveCategory,
              }}
            />
          </List>
        </Box>
        {/* Questions */}
        <Box component="main" className="w-9/12">
          {linkContents}
        </Box>
      </Stack>
    </Container>
  );
};

const LinksWithGuard = () => {
  const query = React.useCallback<(params: undefined) => Promise<LinksP>>(
    async (params: undefined) => {
      const links = await LinkAPI.allLinks({});
      const categories = await LinkAPI.allCategories({});
      return {
        links,
        categories,
      };
    },
    []
  );
  return (
    <QueryGuard
      render={Faq}
      props={{}}
      query={query}
      args={undefined}
      fallback={QueryFallback()}
    />
  );
};

export default LinksWithGuard;
