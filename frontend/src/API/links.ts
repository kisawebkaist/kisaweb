import axios from "axios";

export type LinkT = {
  title: string;
  url: string;
  description: string;
  category: number; // Primary Key for Category
  is_english: boolean;
  requires_sso: boolean;
  external_access: boolean;
  id: number;
};

export type CategoryT = {
  title_category: string;
  title_slug: string;
  id: number;
};

export default class LinkAPI {
  static allLinks(queryParams: Record<string, any>): Promise<LinkT[]> {
    return axios
      .get(
        `${process.env.REACT_APP_API_ENDPOINT}/important-links/`,
        queryParams
      )
      .then((resp) => resp.data);
  }
  static allCategories(queryParams: Record<string, any>): Promise<CategoryT[]> {
    return axios
      .get(
        `${process.env.REACT_APP_API_ENDPOINT}/important-links/category/`,
        queryParams
      )
      .then((resp) => resp.data);
  }
}
