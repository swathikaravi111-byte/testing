import axios, { AxiosInstance, AxiosError } from 'axios';
import { useAuthStore } from '@/store/authStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.request.use((config) => {
      const token = useAuthStore.getState().token;
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          useAuthStore.getState().logout();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async register(email: string, password: string, firstName: string, lastName: string) {
    return this.client.post('/auth/register', {
      email,
      password,
      firstName,
      lastName,
    });
  }

  async login(email: string, password: string) {
    return this.client.post('/auth/login', {
      email,
      password,
    });
  }

  async logout() {
    return this.client.post('/auth/logout');
  }

  // Product endpoints
  async getProducts() {
    return this.client.get('/products');
  }

  async getProductById(id: string) {
    return this.client.get(`/products/${id}`);
  }

  async searchProducts(query: string) {
    return this.client.get(`/products/search/${query}`);
  }

  async filterProducts(filter: any) {
    return this.client.post('/products/filter', filter);
  }

  // Cart endpoints
  async getCart() {
    return this.client.get('/cart');
  }

  async addToCart(productId: string, quantity: number) {
    return this.client.post('/cart/add', {
      productId,
      quantity,
    });
  }

  async updateCartItem(itemId: string, quantity: number) {
    return this.client.put(`/cart/${itemId}`, {
      quantity,
    });
  }

  async removeFromCart(itemId: string) {
    return this.client.delete(`/cart/${itemId}`);
  }

  async clearCart() {
    return this.client.delete('/cart');
  }

  // Order endpoints
  async getOrders() {
    return this.client.get('/orders');
  }

  async getOrderById(id: string) {
    return this.client.get(`/orders/${id}`);
  }

  async createOrder(shippingAddress: string, billingAddress: string, shippingMethod: string) {
    return this.client.post('/orders', {
      shippingAddress,
      billingAddress,
      shippingMethod,
    });
  }

  // Wishlist endpoints
  async getWishlist() {
    return this.client.get('/wishlist');
  }

  async addToWishlist(productId: string) {
    return this.client.post(`/wishlist/${productId}`);
  }

  async removeFromWishlist(productId: string) {
    return this.client.delete(`/wishlist/${productId}`);
  }

  // Review endpoints
  async getProductReviews(productId: string) {
    return this.client.get(`/reviews/product/${productId}`);
  }

  async createReview(productId: string, rating: number, title: string, comment: string) {
    return this.client.post('/reviews', {
      productId,
      rating,
      title,
      comment,
    });
  }

  // Chat endpoints
  async sendChatMessage(message: string) {
    return this.client.post('/chatbot/message', {
      message,
    });
  }

  // User endpoints
  async getUserProfile() {
    return this.client.get('/users/profile');
  }

  async updateUserProfile(data: any) {
    return this.client.put('/users/profile', data);
  }

  // Admin endpoints
  async getDashboard() {
    return this.client.get('/admin/dashboard');
  }

  async getSalesReports() {
    return this.client.get('/admin/reports');
  }
}

export const apiClient = new ApiClient();
