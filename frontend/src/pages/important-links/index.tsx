import { CategoryT, LinkT } from "../../API/links";
import LinkHeader from "../../components/links/LinkHeader";
import LinkEntity from "../../components/links/LinkEntity";
import { LinkCategoryDropdown, LinkCategorySidePanel, LinkSearch } from "../../components/links/LinkSearch";
import QueryGuard from "../../components/common/QueryGuard";
import React from "react";
import { Stack, Typography } from "@mui/material";
import { Container, Box } from "@mui/system";
import Lister from "../../components/common/Lister";
import QueryFallback from "../../components/common/QueryFallback";
import LinkAPI from "../../API/links";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLinkSlash } from "@fortawesome/free-solid-svg-icons";
import ShapeShifter from "../../components/common/ShapeShifter";

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
      return <Lister array={filteredLinks} render={LinkEntity} props={{}} getKey={link => link.id.toString()} />;
    return (
      <Stack className="h-80 gap-y-4">
        <FontAwesomeIcon icon={faLinkSlash} />
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
        <ShapeShifter breakpoint="sm" up={null} down={
          <LinkCategoryDropdown categories={categories} activeCategory={activeCategory} setActiveCategory={setActiveCategory} />
        } />
        <LinkSearch onSearch={setSearchText} />
      </Stack>
      <Stack direction="row" justifyContent="space-between" gap={2}>
        <ShapeShifter breakpoint="sm" down={null} up={
          <LinkCategorySidePanel categories={categories} activeCategory={activeCategory} setActiveCategory={setActiveCategory} />
        } />
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
  return (
    <QueryGuard
      render={ImportantLinks}
      props={{}}
      query={query}
      args={{ linkParam: {}, categoryParam: {} }}
      fallback={QueryFallback()}
    />
  );
};

export default LinksWithGuard;
