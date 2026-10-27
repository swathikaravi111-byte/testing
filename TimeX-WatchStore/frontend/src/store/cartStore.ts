import { create } from 'zustand';
import type { CartItem, Cart } from '@/types';

interface CartState {
  cart: Cart | null;
  setCart: (cart: Cart) => void;
  addItem: (item: CartItem) => void;
  updateItem: (id: string, quantity: number) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
  getItemCount: () => number;
  getTotal: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,

  setCart: (cart: Cart) => {
    set({ cart });
    localStorage.setItem('cart', JSON.stringify(cart));
  },

  addItem: (item: CartItem) => {
    const { cart } = get();
    if (!cart) return;

    const existingItem = cart.items.find((i) => i.id === item.id);
    if (existingItem) {
      existingItem.quantity += item.quantity;
      existingItem.totalPrice = existingItem.unitPrice * existingItem.quantity;
    } else {
      cart.items.push(item);
    }

    cart.totalPrice = cart.items.reduce((sum, i) => sum + i.totalPrice, 0);
    get().setCart(cart);
  },

  updateItem: (id: string, quantity: number) => {
    const { cart } = get();
    if (!cart) return;

    const item = cart.items.find((i) => i.id === id);
    if (item) {
      item.quantity = quantity;
      item.totalPrice = item.unitPrice * quantity;
      cart.totalPrice = cart.items.reduce((sum, i) => sum + i.totalPrice, 0);
      get().setCart(cart);
    }
  },

  removeItem: (id: string) => {
    const { cart } = get();
    if (!cart) return;

    cart.items = cart.items.filter((i) => i.id !== id);
    cart.totalPrice = cart.items.reduce((sum, i) => sum + i.totalPrice, 0);
    get().setCart(cart);
  },

  clearCart: () => {
    set({ cart: null });
    localStorage.removeItem('cart');
  },

  getItemCount: () => {
    const { cart } = get();
    return cart?.items.reduce((sum, item) => sum + item.quantity, 0) || 0;
  },

  getTotal: () => {
    const { cart } = get();
    return cart?.totalPrice || 0;
  },
}));
