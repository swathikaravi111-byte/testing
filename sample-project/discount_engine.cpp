#include <string>
#include <vector>
#include <iostream>

class DiscountEngine {
public:
    double applyDiscount(double price, std::string tier, bool loyalty, int months) {
        double d = 0.0;
        if (tier == "gold") {
            if (loyalty) {
                if (months > 12) {
                    d = 0.25;
                } else {
                    d = 0.15;
                }
            } else {
                d = 0.10;
            }
        } else if (tier == "silver") {
            if (loyalty) {
                d = 0.12;
            } else {
                d = 0.05;
            }
        } else {
            d = 0.0;
        }
        return price * (1.0 - d);
    }

    void logApplied(std::vector<std::string>& entries, std::string label) {
        entries.push_back(label);
        std::cout << "applied " << label << std::endl;
    }
};
