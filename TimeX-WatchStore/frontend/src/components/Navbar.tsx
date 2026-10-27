import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { useCartStore } from '@/store/cartStore';
import { ShoppingCart, LogOut, Menu } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { getItemCount } = useCartStore();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-primary text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="text-2xl font-bold text-accent">
            TimeX
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex space-x-6">
            <Link to="/products" className="hover:text-accent transition">
              Shop
            </Link>
            {isAuthenticated && (
              <>
                <Link to="/orders" className="hover:text-accent transition">
                  Orders
                </Link>
                <Link to="/profile" className="hover:text-accent transition">
                  Profile
                </Link>
                {user?.role === 'Admin' && (
                  <Link to="/admin" className="hover:text-accent transition">
                    Admin
                  </Link>
                )}
              </>
            )}
          </div>

          {/* Right Section */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <div className="text-sm">
                  Welcome, {user?.firstName}
                </div>
                <Link to="/cart" className="relative">
                  <ShoppingCart size={24} />
                  {getItemCount() > 0 && (
                    <span className="absolute -top-2 -right-2 bg-accent text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {getItemCount()}
                    </span>
                  )}
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 hover:text-accent transition"
                >
                  <LogOut size={20} />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 rounded hover:bg-secondary transition"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-secondary rounded hover:bg-indigo-700 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <Menu size={24} />
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <Link
              to="/products"
              className="block hover:text-accent transition"
              onClick={() => setMobileMenuOpen(false)}
            >
              Shop
            </Link>
            {isAuthenticated && (
              <>
                <Link
                  to="/orders"
                  className="block hover:text-accent transition"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Orders
                </Link>
                <Link
                  to="/profile"
                  className="block hover:text-accent transition"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Profile
                </Link>
              </>
            )}
            <Link
              to="/cart"
              className="block hover:text-accent transition flex items-center space-x-2"
              onClick={() => setMobileMenuOpen(false)}
            >
              <ShoppingCart size={20} />
              <span>Cart ({getItemCount()})</span>
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
