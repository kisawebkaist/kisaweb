import { IconButton, InputAdornment, List, ListItemButton, MenuItem, Select, SelectChangeEvent, SvgIcon, SxProps, TextField, Theme } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons"
import { CategoryT } from "../../API/links";
import { useTheme } from "@mui/material";

type LinkSearchProps = {
  onSearch: Function;
};

export const LinkSearch = ({ onSearch }: LinkSearchProps) => {
  const theme = useTheme();

  return (
    <TextField
      fullWidth
      autoFocus
      variant="filled"
      type="search"
      label="Search"
      onChange={(e) => onSearch(e.target.value)}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <SvgIcon>
              <FontAwesomeIcon
                  icon={faSearch}
                />
            </SvgIcon>
          </InputAdornment>
        ),
      }}
      sx={{
        backgroundColor: theme.vars.palette.background.paper, 
      }}
    />
  );
};

type LinkCategoryProps = {
  categories: CategoryT[];
  activeCategory: number;
  setActiveCategory: (id: number) => void;
}
const categoryAll: CategoryT = {
  title_category: "All",
  title_slug: "all",
  id: -1,
}

export const LinkCategoryDropdown = ({ categories, activeCategory, setActiveCategory }: LinkCategoryProps) => {
  const theme = useTheme();
  const renderEntry = (category: CategoryT) => (
    <MenuItem value={category.id} key={category.id}>{category.title_category}</MenuItem>
  );
  const handleChange = (event: SelectChangeEvent) => {
    setActiveCategory(parseInt(event.target.value));
  };

  return (
    <Select
      variant="filled"
      value={activeCategory.toString()}
      label="Category"
      onChange={handleChange}
      sx={{
        backgroundColor: theme.vars.palette.background.paper, // TODO: fix this
      }}
    >
      {[categoryAll].concat(categories).map(renderEntry)}
    </Select>
  );
};

export const LinkCategorySidePanel = ({ categories, activeCategory, setActiveCategory }: LinkCategoryProps) => (
  <List
    component="nav"
    sx={{ width: "20%", marginRight: "2" }}
  >
    {
      [categoryAll]
        .concat(categories)
        .map(
          (category) => (
            <ListItemButton
              selected={activeCategory === category.id}
              onClick={() => setActiveCategory(category.id)}
              key={category.id}
            >
              {category.title_category}
            </ListItemButton>
          )
        )
      }
  </List>
);
