import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '@/services/api';

export default function CheckoutPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    shippingAddress: '',
    billingAddress: '',
    shippingMethod: 'standard',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await apiClient.createOrder(
        formData.shippingAddress,
        formData.billingAddress,
        formData.shippingMethod
      );
      alert('Order created successfully!');
      navigate(`/orders`);
    } catch (error) {
      alert('Failed to create order');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Checkout</h1>

      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto bg-white rounded-lg shadow p-8">
        <div className="mb-6">
          <label className="block text-sm font-bold mb-2">Shipping Address</label>
          <input
            type="text"
            required
            value={formData.shippingAddress}
            onChange={(e) => setFormData({ ...formData, shippingAddress: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary"
            placeholder="Enter your shipping address"
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-bold mb-2">Billing Address</label>
          <input
            type="text"
            required
            value={formData.billingAddress}
            onChange={(e) => setFormData({ ...formData, billingAddress: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary"
            placeholder="Enter your billing address"
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-bold mb-2">Shipping Method</label>
          <select
            value={formData.shippingMethod}
            onChange={(e) => setFormData({ ...formData, shippingMethod: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary"
          >
            <option value="standard">Standard (5-7 days)</option>
            <option value="express">Express (2-3 days)</option>
            <option value="overnight">Overnight</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full"
        >
          {loading ? 'Processing...' : 'Place Order'}
        </button>
      </form>
    </div>
  );
}
