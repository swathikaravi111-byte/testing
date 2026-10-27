export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'Customer' | 'Admin' | 'Support';
}

export interface Product {
  id: string;
  name: string;
  description: string;
  sku: string;
  price: number;
  discountPrice?: number;
  brand: string;
  category: string;
  model: string;
  waterResistance: string;
  material: string;
  movement: string;
  diameter: string;
  color: string;
  averageRating: number;
  totalReviews: number;
  imageUrl?: string;
}

export interface CartItem {
  id: string;
  productId: string;
  productName: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
}

export interface Cart {
  userId: string;
  items: CartItem[];
  totalPrice: number;
}

export interface Order {
  id: string;
  orderNumber: string;
  status: 'Pending' | 'Processing' | 'Shipped' | 'Delivered' | 'Cancelled' | 'Returned';
  totalAmount: number;
  taxAmount: number;
  shippingCost: number;
  shippingAddress: string;
  createdAt: string;
  items: OrderItem[];
}

export interface OrderItem {
  productId: string;
  productName: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
}

export interface Review {
  id: string;
  rating: number;
  title: string;
  comment: string;
  userName: string;
  createdAt: string;
}

export interface WishlistItem {
  productId: string;
  productName: string;
  price: number;
  imageUrl?: string;
}

export interface AuthResponse {
  isSuccess: boolean;
  message: string;
  user?: User;
  token?: string;
  refreshToken?: string;
}
