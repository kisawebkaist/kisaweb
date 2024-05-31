import axios from "axios";

export type FaqT = {
  question: string;
  timestamp: string; // Datetime string
  category: number; // Primary Key
  answer: string;
  id: number;
};

export type CategoryT = {
  title_category: string;
  title_slug: string;
  id: number;
};

export default class FaqAPI {
  static allFaqs(queryParams: Record<string, any>): Promise<FaqT[]> {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}/faq/`, queryParams)
      .then((resp) => resp.data);
  }
  static allCategories(queryParams: Record<string, any>): Promise<CategoryT[]> {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}/faq/category/`, queryParams)
      .then((resp) => resp.data);
  }
}
