import { CategoryT, LinkT } from "../API/links";
import LinkHeader from "../components/links/LinkHeader";
import LinkEntity from "../components/links/LinkEntity";
import { LinkCategoryDropdown, LinkCategorySidePanel, LinkSearch } from "../components/links/LinkSearch";
import QueryGuard from "../components/query-guard";
import React from "react";
import { Stack, Typography } from "@mui/material";
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

const ImportantLinks = ({ links, categories }: LinksP) => {
  const [searchText, setSearchText] = React.useState<string>("");
  const [activeCategory, setActiveCategory] = React.useState<number>(-1);
  const [filteredLinks, setFilteredLinks] = React.useState<LinkT[]>(links);

  React.useEffect(() => {
    const matchesActiveCategory = (link: LinkT) => activeCategory === -1 || activeCategory === link.category;
    const matchesSearchText = (link: LinkT) => {
      const searchTextLower = searchText.toLowerCase();
      return searchTextLower === "" || link.title.toLowerCase().includes(searchTextLower) || link.description.toLowerCase().includes(searchTextLower);
    };

    setFilteredLinks(links.filter(matchesActiveCategory).filter(matchesSearchText));
  }, [activeCategory, searchText, links]);

  const linkContents = React.useMemo(() => {
    if (filteredLinks.length !== 0)
      return <Lister array={filteredLinks} render={LinkEntity} props={{}} />;
    return (
      <Stack className="h-80 gap-y-4">
        <FontAwesomeIcon icon = {faLinkSlash}/>
        <Typography variant="body2" textAlign="center">
          No Links Found.
        </Typography>
      </Stack>
    );
  }, [filteredLinks]);

  return (
    <Container maxWidth="md">
      <LinkHeader />
      <Stack>
        <LinkCategoryDropdown categories={categories} activeCategory={activeCategory} setActiveCategory={setActiveCategory} sx={{ display: {xs: "block", sm: "none"} }}/>
        <LinkSearch onSearch={setSearchText} />
      </Stack>
      <Stack direction="row" justifyContent="space-between">
        <LinkCategorySidePanel categories={categories} activeCategory={activeCategory} setActiveCategory={setActiveCategory} sx={{ display: {xs: "none", sm: "block"}, width: "20%", marginRight: "2" }} />
        {/* Questions */}
        <Box component="main" sx={{ flex: 1 }}>
          {linkContents}
        </Box>
      </Stack>
    </Container>
  );
};

const LinksWithGuard = () => {
  type QueryParams = {
    linkParam: Record<string, any>,
    categoryParam: Record<string, any>,
  }
  async function query(args: QueryParams) {
    return {
        links: await LinkAPI.allLinks(args.linkParam),
        categories: await LinkAPI.allCategories(args.categoryParam)
    };
  }
  // QueryGuard memorization is not working when switching tabs prolly due to being rerendered from scratch
  return (
    <QueryGuard
      render={ImportantLinks}
      props={{}}
      query={query}
      args={{linkParam: {}, categoryParam: {}}}
      fallback={QueryFallback()}
    />
  );
};

export default LinksWithGuard;
