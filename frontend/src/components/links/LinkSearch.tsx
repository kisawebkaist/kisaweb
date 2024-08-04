import { IconButton, InputAdornment, List, ListItemButton, MenuItem, Select, SelectChangeEvent, SxProps, TextField, Theme } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons"
import { CategoryT } from "../../API/links";

type LinkSearchProps = {
  onSearch: Function;
};

export const LinkSearch = ({ onSearch }: LinkSearchProps) => {
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
            <IconButton>
              <FontAwesomeIcon
                icon={faSearch}
                className="transition-colors hover:text-black"
              />
            </IconButton>
          </InputAdornment>
        ),
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
  const renderEntry = (category: CategoryT) => (
    <MenuItem value={category.id}>{category.title_category}</MenuItem>
  );
  const handleChange = (event: SelectChangeEvent) => {
    setActiveCategory(parseInt(event.target.value));
  };

  return (
    <Select
      value={activeCategory.toString()}
      label="Category"
      onChange={handleChange}
    >
      {[categoryAll].concat(categories).map(renderEntry)}
    </Select>
  );
};

export const LinkCategorySidePanel = ({ categories, activeCategory, setActiveCategory }: LinkCategoryProps) => {
  const renderEntry = (category: CategoryT) => (
    <ListItemButton
      selected={activeCategory === category.id}
      onClick={() => setActiveCategory(category.id)}
    >
      {category.title_category}
    </ListItemButton>
  );

  return (
    <List
      component="nav"
      sx={{ width: "20%", marginRight: "2" }}
    >
      {[categoryAll].concat(categories).map(renderEntry)}
    </List>
  );
};
