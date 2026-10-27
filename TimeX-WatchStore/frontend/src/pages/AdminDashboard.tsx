import { useEffect, useState } from 'react';
import { apiClient } from '@/services/api';
import { Users, ShoppingCart, DollarSign, TrendingUp } from 'lucide-react';

export default function AdminDashboard() {
  const [dashboard, setDashboard] = useState<any>(null);
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const dashResponse = await apiClient.getDashboard();
        setDashboard(dashResponse.data);

        const reportsResponse = await apiClient.getSalesReports();
        setReports(reportsResponse.data);
      } catch (error) {
        console.error('Failed to fetch dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="container mx-auto px-4 py-8 text-center">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      {/* Stats */}
      {dashboard && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Users</p>
                <p className="text-3xl font-bold">{dashboard.totalUsers}</p>
              </div>
              <Users size={32} className="text-secondary" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Products</p>
                <p className="text-3xl font-bold">{dashboard.totalProducts}</p>
              </div>
              <ShoppingCart size={32} className="text-secondary" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Orders</p>
                <p className="text-3xl font-bold">{dashboard.totalOrders}</p>
              </div>
              <ShoppingCart size={32} className="text-secondary" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Revenue</p>
                <p className="text-3xl font-bold">${dashboard.totalRevenue.toFixed(2)}</p>
              </div>
              <DollarSign size={32} className="text-secondary" />
            </div>
          </div>
        </div>
      )}

      {/* Sales Report */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
          <TrendingUp size={24} />
          Sales Report
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b">
              <tr>
                <th className="text-left py-2">Date</th>
                <th className="text-right py-2">Orders</th>
                <th className="text-right py-2">Sales</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((report) => (
                <tr key={report.date} className="border-b hover:bg-gray-50">
                  <td className="py-2">
                    {new Date(report.date).toLocaleDateString()}
                  </td>
                  <td className="text-right">{report.orderCount}</td>
                  <td className="text-right font-semibold">
                    ${report.totalSales.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
