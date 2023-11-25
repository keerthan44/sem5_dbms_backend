from django.apps import AppConfig
from django.db import connection

class AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auction'
    def ready(self):
        cursor = connection.cursor()
        cursor.execute(
            r'''
            CREATE PROCEDURE IF NOT EXISTS update_auction_status()
            BEGIN
                
                SET @current_time = NOW();

                UPDATE auction_auction
                SET status = CASE
                    WHEN current_time < startDate THEN 'not begun'
                    WHEN current_time >= startDate AND current_time <= endDate THEN 'started'
                    ELSE 'over'
                END;
            END;            '''
        )
        cursor.execute(
            r'''
            CREATE FUNCTION IF NOT EXISTS calculate_total_bid_amount(auction_id INT)
            RETURNS INT
            BEGIN
                DECLARE total_amount INT;
                
                SELECT COALESCE(SUM(amount), 0)
                INTO total_amount
                FROM auction_bids
                WHERE item_id IN (SELECT id FROM auction_item WHERE auction_id = auction_id);

                RETURN total_amount;
            END;
            '''
        )
        cursor.execute(
            '''
            CREATE TRIGGER IF NOT EXISTS update_bid_count_trigger
            AFTER INSERT ON auction_bids
            FOR EACH ROW
            BEGIN
                -- Update bidCount in the Item table for the corresponding item
                UPDATE auction_item
                SET bidCount = bidCount + 1
                WHERE id = NEW.item_id;
            END;
            '''
        )
        cursor.close() 
