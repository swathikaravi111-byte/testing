import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { apiClient } from '@/services/api';
import type { Cart } from '@/types';
import { Trash2 } from 'lucide-react';

export default function CartPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const response = await apiClient.getCart();
        setCart(response.data);
      } catch (error) {
        console.error('Failed to fetch cart:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, []);

  const handleUpdateQuantity = async (itemId: string, quantity: number) => {
    try {
      await apiClient.updateCartItem(itemId, quantity);
      if (cart) {
        const item = cart.items.find((i) => i.id === itemId);
        if (item) {
          item.quantity = quantity;
          item.totalPrice = item.unitPrice * quantity;
          cart.totalPrice = cart.items.reduce((sum, i) => sum + i.totalPrice, 0);
          setCart({ ...cart });
        }
      }
    } catch (error) {
      console.error('Failed to update cart:', error);
    }
  };

  const handleRemoveItem = async (itemId: string) => {
    try {
      await apiClient.removeFromCart(itemId);
      if (cart) {
        cart.items = cart.items.filter((i) => i.id !== itemId);
        cart.totalPrice = cart.items.reduce((sum, i) => sum + i.totalPrice, 0);
        setCart({ ...cart });
      }
    } catch (error) {
      console.error('Failed to remove item:', error);
    }
  };

  if (loading) {
    return <div className="container mx-auto px-4 py-8 text-center">Loading...</div>;
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <h1 className="text-2xl font-bold mb-4">Your Cart is Empty</h1>
        <Link to="/products" className="btn-primary">
          Continue Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow">
            {cart.items.map((item) => (
              <div
                key={item.id}
                className="flex justify-between items-center p-6 border-b last:border-b-0"
              >
                <div className="flex-1">
                  <h3 className="font-bold mb-2">{item.productName}</h3>
                  <p className="text-gray-600">${item.unitPrice}</p>
                </div>

                <div className="flex items-center border border-gray-300 rounded-lg mx-4">
                  <button
                    onClick={() => handleUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
                    className="px-3 py-2"
                  >
                    -
                  </button>
                  <input
                    type="number"
                    value={item.quantity}
                    onChange={(e) => handleUpdateQuantity(item.id, parseInt(e.target.value) || 1)}
                    className="w-12 text-center border-l border-r"
                  />
                  <button
                    onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                    className="px-3 py-2"
                  >
                    +
                  </button>
                </div>

                <div className="text-right mr-4">
                  <p className="font-bold">${item.totalPrice}</p>
                </div>

                <button
                  onClick={() => handleRemoveItem(item.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="bg-gray-50 rounded-lg p-6 h-fit">
          <h2 className="text-xl font-bold mb-6">Order Summary</h2>

          <div className="space-y-4 mb-6">
            <div className="flex justify-between">
              <span className="text-gray-600">Subtotal</span>
              <span className="font-semibold">${cart.totalPrice.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tax (10%)</span>
              <span className="font-semibold">${(cart.totalPrice * 0.1).toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Shipping</span>
              <span className="font-semibold">$10.00</span>
            </div>
          </div>

          <div className="border-t pt-4 mb-6">
            <div className="flex justify-between">
              <span className="font-bold">Total</span>
              <span className="text-2xl font-bold text-accent">
                ${(cart.totalPrice * 1.1 + 10).toFixed(2)}
              </span>
            </div>
          </div>

          <button
            onClick={() => navigate('/checkout')}
            className="btn-primary w-full"
          >
            Proceed to Checkout
          </button>
        </div>
      </div>
    </div>
  );
}
