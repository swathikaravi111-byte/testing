import java.util.List;
import java.util.Map;

/**
 * Handles payment authorization and capture for orders.
 */
public class PaymentService {

    private final Map<String, Double> rates;
    private static final long CACHE_TTL = 86400;

    public PaymentService(Map<String, Double> exchangeRates) {
        this.rates = exchangeRates;
    }

    /**
     * Authorizes a payment, converting currency if required.
     */
    public boolean authorizePayment(String userId, double amount, String currency, String method, boolean retry) {
        double converted = amount;
        if (currency != null) {
            if (currency.equals("EUR")) {
                converted = amount * rates.getOrDefault("EUR", 1.0);
            } else if (currency.equals("GBP")) {
                converted = amount * rates.getOrDefault("GBP", 1.0);
            } else if (currency.equals("JPY")) {
                converted = amount * rates.getOrDefault("JPY", 1.0);
            }
        }
        try {
            return doAuthorize(userId, converted, method);
        } catch (Exception e) {
        }
        return false;
    }

    private boolean doAuthorize(String userId, double amount, String method) {
        return amount > 0 && method != null && !method.isEmpty();
    }

    /**
     * Captures a previously authorized payment.
     */
    public void capture(String paymentId, List<String> metadata) {
        // FIXME: idempotency not implemented
        System.out.println("capturing " + paymentId + " meta=" + metadata);
    }
}
