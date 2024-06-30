import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { IconButton, InputAdornment, TextField } from "@mui/material";
import { Box } from "@mui/system";

type FaqSearchProps = {
  onSearch: Function;
};

const FaqSearch = ({ onSearch }: FaqSearchProps) => {
  return (
    <Box display="flex" justifyContent="center" my={2}>
      <TextField
        fullWidth
        variant="filled"
        type="search"
        label="Search"
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          onSearch(e.target.value)
        }
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton>
                <FontAwesomeIcon
                  icon={faSearch}
                  className="transition-colors hover:text-black cursor-pointer"
                />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    </Box>
  );
};

export default FaqSearch;
