import { IconButton, InputAdornment, TextField } from "@mui/material";
import { Box } from "@mui/system";
import SearchIcon from "@mui/icons-material/Search";

type LinkSearchProps = {
  onSearch: Function;
};

const LinkSearch = ({ onSearch }: LinkSearchProps) => {
  return (
    <Box display="flex" justifyContent="center" my={2}>
      <TextField
        fullWidth
        variant="filled"
        type="search"
        label="Search"
        onChange={(e) => onSearch(e.target.value)}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton >
                <SearchIcon
                  sx={{
                    transition: "color 0.1s ease-in",
                    "&:hover": {
                      cursor: "pointer",
                      color: "black",
                    },
                  }}
                />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    </Box>
  );
};

export default LinkSearch;
