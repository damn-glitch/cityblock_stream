// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTrading {

    struct Offer {
        uint id;
        address seller;
        uint energyAmount;
        uint pricePerKWh;
        bool available;
    }

    struct Demand {
        uint id;
        address buyer;
        uint energyAmount;
        uint maxPricePerKWh;
    }

    struct Trade {
        uint tradeId;
        uint offerId;
        uint demandId;
        uint energyTransferred;
        uint pricePerKWh;
        address seller;
        address buyer;
    }

    Offer[] public offers;
    Demand[] public demands;
    Trade[] public trades;

    event OfferCreated(uint offerId, address seller, uint energyAmount, uint pricePerKWh);
    event DemandExpressed(uint demandId, address buyer, uint energyAmount, uint maxPricePerKWh);
    event TradeMatched(uint tradeId, uint offerId, uint demandId, address seller, address buyer, uint energyTransferred, uint pricePerKWh);

    function createOffer(uint _energyAmount, uint _pricePerKWh) public {
        uint offerId = offers.length + 1;
        offers.push(Offer(offerId, msg.sender, _energyAmount, _pricePerKWh, true));
        emit OfferCreated(offerId, msg.sender, _energyAmount, _pricePerKWh);
    }

    function expressDemand(uint _energyAmount, uint _maxPricePerKWh) public {
        uint demandId = demands.length + 1;
        demands.push(Demand(demandId, msg.sender, _energyAmount, _maxPricePerKWh));
        emit DemandExpressed(demandId, msg.sender, _energyAmount, _maxPricePerKWh);
    }

    function matchTrades() public {
        for (uint i = 0; i < demands.length; i++) {
            for (uint j = 0; j < offers.length; j++) {
                if (offers[j].available && offers[j].energyAmount >= demands[i].energyAmount && offers[j].pricePerKWh <= demands[i].maxPricePerKWh) {
                    uint tradeId = trades.length + 1;
                    trades.push(Trade(tradeId, offers[j].id, demands[i].id, demands[i].energyAmount, offers[j].pricePerKWh, offers[j].seller, demands[i].buyer));
                    offers[j].available = false; // Mark the offer as not available
                    emit TradeMatched(tradeId, offers[j].id, demands[i].id, offers[j].seller, demands[i].buyer, demands[i].energyAmount, offers[j].pricePerKWh);
                    break;
                }
            }
        }
    }
}
