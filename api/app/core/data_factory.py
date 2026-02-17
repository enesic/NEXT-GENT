"""
Data Factory Architecture for NextGent CRM
Generates realistic, production-grade test data using Faker library
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import UUID
import random
import hashlib
from faker import Faker

# Initialize Faker with Turkish locale
fake_tr = Faker('tr_TR')
fake_en = Faker('en_US')


class BaseFactory:
    """Base factory class with common utilities"""
    
    @staticmethod
    def weighted_choice(choices: List[tuple]) -> Any:
        """Select from weighted choices. Each choice is (value, weight)"""
        values, weights = zip(*choices)
        total = sum(weights)
        normalized = [w/total for w in weights]
        return random.choices(values, weights=normalized)[0]
    
    @staticmethod
    def random_datetime_in_range(start: datetime, end: datetime) -> datetime:
        """Generate random datetime between start and end"""
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)
    
    @staticmethod
    def business_hours_datetime(base_date: datetime) -> datetime:
        """Generate datetime during business hours (9 AM - 6 PM)"""
        # 60% chance during business hours, 40% outside
        if random.random() < 0.6:
            hour = random.randint(9, 17)
        else:
            hour = random.choice(list(range(0, 9)) + list(range(18, 24)))
        
        minute = random.choice([0, 15, 30, 45])
        return base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)


class CustomerFactory(BaseFactory):
    """Factory for generating realistic customer data"""
    
    SEGMENT_DISTRIBUTION = [
        ('VIP', 0.20),
        ('GOLD', 0.30),
        ('SILVER', 0.30),
        ('REGULAR', 0.20)
    ]
    
    def __init__(self, faker_instance: Faker = fake_tr):
        self.fake = faker_instance
    
    def generate_batch(self, count: int, tenant_id: UUID, sector: str) -> List[Dict]:
        """Generate batch of realistic customers"""
        customers = []
        sector_code = self._get_sector_code(sector)
        
        for i in range(count):
            segment = self.weighted_choice(self.SEGMENT_DISTRIBUTION)
            customer = self._create_customer(i + 1, tenant_id, sector_code, segment)
            customers.append(customer)
        
        return customers
    
    def _create_customer(self, index: int, tenant_id: UUID, sector_code: str, segment: str) -> Dict:
        """Create single customer with realistic data"""
        import bcrypt
        
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        
        # Generate realistic email
        email_domain = self._get_sector_email_domain(sector_code)
        email = f"{first_name.lower()}.{last_name.lower()}{index}@{email_domain}"
        
        # Generate metrics based on segment
        total_spent, total_orders = self._generate_segment_metrics(segment)
        
        # Turkish phone number format
        phone_number = f"+905{random.randint(300000000, 599999999)}"
        phone_hash = hashlib.sha256(phone_number.encode()).hexdigest()
        
        # Generate join date (last 180 days, weighted toward recent)
        days_ago = int(random.triangular(0, 180, 30))  # Weighted toward recent
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        return {
            'id': None,  # Will be set by database
            'tenant_id': str(tenant_id),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'customer_id': f"{sector_code}-{str(index).zfill(6)}",
            'pin_hash': bcrypt.hashpw("1234".encode(), bcrypt.gensalt()).decode(),
            'phone_hash': phone_hash,
            'segment': segment,
            'status': 'ACTIVE',
            'total_orders': total_orders,
            'total_spent': round(total_spent, 2),
            'lifetime_value': round(total_spent * 1.2, 2),
            'notes': f"{sector_code} sektöründen müşteri",
            'created_at': created_at,
            'updated_at': created_at
        }
    
    @staticmethod
    def _get_sector_code(sector: str) -> str:
        """Get 3-letter sector code"""
        codes = {
            "medical": "MED", "legal": "LEG", "real_estate": "EST",
            "manufacturing": "MFG", "ecommerce": "ECM", "education": "EDU",
            "finance": "FIN", "hospitality": "HOS", "automotive": "AUT",
            "retail": "RTL", "beauty": "BEA"
        }
        return codes.get(sector, "GEN")
    
    @staticmethod
    def _get_sector_email_domain(sector_code: str) -> str:
        """Get realistic email domain for sector"""
        domains = {
            "MED": "hospital.com", "LEG": "lawfirm.com", "EST": "realty.com",
            "MFG": "factory.com", "ECM": "shop.com", "EDU": "school.com",
            "FIN": "bank.com", "HTL": "hotel.com", "AUTO": "dealer.com",
            "RTL": "store.com"
        }
        return domains.get(sector_code, "example.com")
    
    @staticmethod
    def _generate_segment_metrics(segment: str) -> tuple:
        """Generate realistic total_spent and total_orders based on segment"""
        if segment == 'VIP':
            spent = random.uniform(15000, 50000)
            orders = random.randint(60, 150)
        elif segment == 'GOLD':
            spent = random.uniform(7000, 15000)
            orders = random.randint(30, 60)
        elif segment == 'SILVER':
            spent = random.uniform(2000, 7000)
            orders = random.randint(15, 30)
        else:  # REGULAR
            spent = random.uniform(100, 2000)
            orders = random.randint(1, 15)
        
        return spent, orders


class InteractionFactory(BaseFactory):
    """Factory for generating realistic interactions/appointments"""
    
    SECTOR_TYPES = {
        "medical": ["Kontrol", "İlk Muayene", "Tahlil", "Tedavi", "Aşı"],
        "legal": ["Danışma", "Dava Takibi", "Sözleşme", "Arabuluculuk", "Mahkeme"],
        "real_estate": ["Konut Gezisi", "Ofis Gezisi", "Değerleme", "Sözleşme", "Teslim"],
        "manufacturing": ["Üretim Planlama", "Kalite Kontrol", "Bakım", "Tedarik", "Sevkiyat"],
        "ecommerce": ["Sipariş Takibi", "İade", "Müşteri Desteği", "Ürün Danışma", "Kargo"],
        "education": ["Ders", "Sınav", "Veli Görüşmesi", "Danışmanlık", "Etkinlik"],
        "finance": ["Kredi Başvuru", "Yatırım Danışma", "Hesap Açma", "Sigorta", "Bütçe"],
        "hospitality": ["Rezervasyon", "Check-in", "Etkinlik", "Spa", "Restoran"],
        "automotive": ["Test Sürüşü", "Servis", "Bakım", "Satış", "Aksesuar"],
        "retail": ["Satış", "Değişim", "Danışma", "Stok Bilgi", "Kampanya"]
    }
    
    STATUS_DISTRIBUTION = [
        ('COMPLETED', 0.50),
        ('CONFIRMED', 0.30),
        ('PENDING', 0.15),
        ('CANCELLED', 0.05)
    ]
    
    def generate_for_sector(
        self, 
        count: int, 
        tenant_id: UUID, 
        sector: str, 
        customers: List[Dict],
        days_back: int = 30
    ) -> List[Dict]:
        """Generate interactions for a sector"""
        interactions = []
        sector_types = self.SECTOR_TYPES.get(sector, self.SECTOR_TYPES["medical"])
        base_time = datetime.utcnow()
        
        # Track used time slots to prevent overlapping
        used_time_slots = set()
        
        for i in range(count):
            max_attempts = 10
            start_time = None
            end_time = None
            
            # Try to find a unique time slot
            for attempt in range(max_attempts):
                # Random date within range
                days_ago = random.randint(0, days_back)
                target_date = base_time - timedelta(days=days_ago)
                
                # Business hours datetime
                temp_start = self.business_hours_datetime(target_date)
                duration_minutes = random.choice([30, 45, 60])
                temp_end = temp_start + timedelta(minutes=duration_minutes)
                
                # Create a unique key for this time slot
                time_key = (temp_start.isoformat(), temp_end.isoformat())
                
                # Check if this slot is already used
                if time_key not in used_time_slots:
                    start_time = temp_start
                    end_time = temp_end
                    used_time_slots.add(time_key)
                    break
                
                # If we can't find a slot, add some random seconds to make it unique
                if attempt == max_attempts - 1:
                    start_time = temp_start + timedelta(seconds=random.randint(0, 300))
                    duration_minutes = random.choice([30, 45, 60])
                    end_time = start_time + timedelta(minutes=duration_minutes)
            
            # Status based on age
            days_ago = (base_time - start_time).days
            if days_ago > 7:
                status = self.weighted_choice([('COMPLETED', 0.85), ('CANCELLED', 0.15)])
            elif days_ago > 0:
                status = 'CONFIRMED'
            else:
                status = self.weighted_choice([('CONFIRMED', 0.7), ('PENDING', 0.3)])
            
            # Random customer
            customer = random.choice(customers)
            
            interaction = {
                'id': None,
                'tenant_id': str(tenant_id),
                'title': random.choice(sector_types),
                'description': f"Otomatik oluşturulmuş {sector} randevusu",
                'type': random.choice(sector_types).lower().replace(' ', '_'),
                'start_time': start_time,
                'end_time': end_time,
                'client_name': f"{customer['first_name']} {customer['last_name']}",
                'client_email': customer['email'],
                'client_phone': f"+905{random.randint(300000000, 599999999)}",
                'status': status,
                'created_at': start_time - timedelta(days=random.randint(1, 5)),
                'updated_at': start_time - timedelta(days=random.randint(0, 2))
            }
            interactions.append(interaction)
        
        return interactions


class VAPICallFactory(BaseFactory):
    """Factory for generating VAPI call records with realistic transcripts"""
    
    CALL_STATUS_DISTRIBUTION = [
        ('completed', 0.70),
        ('resolved_ai', 0.15),
        ('transferred_human', 0.10),
        ('failed', 0.05)
    ]
    
    SENTIMENT_DISTRIBUTION = [
        ('positive', 0.70),
        ('neutral', 0.20),
        ('negative', 0.10)
    ]
    
    def create_from_interaction(
        self,
        interaction: Dict,
        tenant_id: UUID,
        customer_phone: str
    ) -> Optional[Dict]:
        """Create VAPI call record from interaction (80% chance)"""
        if random.random() > 0.8:
            return None
        
        call_status = self.weighted_choice(self.CALL_STATUS_DISTRIBUTION)
        sentiment = self.weighted_choice(self.SENTIMENT_DISTRIBUTION)
        
        # Call duration based on status
        if call_status == 'failed':
            duration = random.randint(5, 30)
        elif call_status == 'resolved_ai':
            duration = random.randint(60, 180)
        else:
            duration = random.randint(120, 600)
        
        started_at = interaction['start_time'] - timedelta(minutes=random.randint(0, 15))
        ended_at = started_at + timedelta(seconds=duration)
        
        # Generate transcript
        transcript = self._generate_transcript(interaction['title'], sentiment, call_status)
        
        # Sentiment score
        if sentiment == 'positive':
            sentiment_score = random.uniform(0.7, 1.0)
        elif sentiment == 'neutral':
            sentiment_score = random.uniform(0.4, 0.6)
        else:
            sentiment_score = random.uniform(0.0, 0.3)
        
        return {
            'id': None,
            'tenant_id': str(tenant_id),
            'vapi_call_id': f"vapi_{fake_en.uuid4()}",
            'caller_name_encrypted': interaction['client_name'],  # Would be encrypted in real implementation
            'caller_phone_encrypted': customer_phone,
            'phone_hash': hashlib.sha256(customer_phone.encode()).hexdigest(),
            'transcript_encrypted': transcript,
            'call_duration_seconds': duration,
            'call_status': call_status,
            'sentiment': sentiment,
            'sentiment_score': round(sentiment_score, 2),
            'ai_confidence_score': random.uniform(0.75, 0.98) if call_status != 'failed' else None,
            'call_quality_score': random.randint(3, 5) if call_status != 'failed' else random.randint(1, 3),
            'started_at': started_at,
            'ended_at': ended_at,
            'created_at': started_at,
            'updated_at': ended_at
        }
    
    @staticmethod
    def _generate_transcript(interaction_type: str, sentiment: str, status: str) -> str:
        """Generate realistic call transcript"""
        if status == 'failed':
            return "Arama bağlantı hatası nedeniyle sonlandırıldı."
        
        intro = f"Müşteri Asistanı: Merhaba, {interaction_type} konusunda nasıl yardımcı olabilirim?"
        
        if sentiment == 'positive':
            response = f"Müşteri: Merhaba, {interaction_type.lower()} için randevu almak istiyorum. Asistan: Tabii ki, size uygun bir tarih ayarlayalım."
        elif sentiment == 'neutral':
            response = f"Müşteri: {interaction_type} hakkında bilgi almak istiyorum. Asistan: Size detaylı bilgi vereyim."
        else:
            response = f"Müşteri: Randevum iptal oldu, çok memnun değilim. Asistan: Özür dileriz, sorunu çözelim."
        
        return f"{intro}\n{response}\n... (görüşme devam ediyor)"


class TokenUsageFactory(BaseFactory):
    """Factory for generating token usage records"""
    
    MODEL_DISTRIBUTION = [
        ('gpt-4-turbo', 0.60),
        ('gpt-3.5-turbo', 0.30),
        ('claude-3-sonnet', 0.10)
    ]
    
    @staticmethod
    def create_for_call(call: Dict, tenant_id: UUID) -> Dict:
        """Create token usage record for a VAPI call"""
        model = BaseFactory.weighted_choice(TokenUsageFactory.MODEL_DISTRIBUTION)
        
        # Estimate tokens based on call duration
        duration = call['call_duration_seconds']
        base_tokens = int(duration / 2)  # Rough estimate
        
        tokens_prompt = int(base_tokens * random.uniform(0.4, 0.6))
        tokens_completion = int(base_tokens * random.uniform(0.4, 0.6))
        total_tokens = tokens_prompt + tokens_completion
        
        # Calculate cost
        estimated_cost = TokenUsageFactory._calculate_cost(model, tokens_prompt, tokens_completion)
        
        return {
            'id': None,
            'tenant_id': str(tenant_id),
            'call_id': call['id'],  # Will be set after call is inserted
            'model_name': model,
            'tokens_prompt': tokens_prompt,
            'tokens_completion': tokens_completion,
            'total_tokens': total_tokens,
            'estimated_cost': round(estimated_cost, 6),
            'call_duration_seconds': duration,
            'success': call['call_status'] != 'failed',
            'created_at': call['ended_at'],
            'updated_at': call['ended_at']
        }
    
    @staticmethod
    def _calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate estimated cost based on model pricing"""
        pricing = {
            "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
            "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
            "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
        }
        
        model_pricing = pricing.get(model, {"prompt": 0.001, "completion": 0.002})
        prompt_cost = (prompt_tokens / 1000) * model_pricing["prompt"]
        completion_cost = (completion_tokens / 1000) * model_pricing["completion"]
        
        return prompt_cost + completion_cost


class SatisfactionFactory(BaseFactory):
    """Factory for generating satisfaction survey responses"""
    
    def create_for_interaction(
        self,
        interaction: Dict,
        tenant_id: UUID
    ) -> Optional[Dict]:
        """Create satisfaction response for completed interaction (60% response rate)"""
        if interaction['status'] != 'COMPLETED' or random.random() > 0.6:
            return None
        
        # CSAT rating (1-5)
        csat = self.weighted_choice([
            (5, 0.35),
            (4, 0.30),
            (3, 0.20),
            (2, 0.10),
            (1, 0.05)
        ])
        
        # NPS score (0-10)
        if csat >= 4:
            nps = random.randint(8, 10)
            sentiment = 'positive'
            score = random.uniform(0.7, 1.0)
        elif csat == 3:
            nps = random.randint(5, 7)
            sentiment = 'neutral'
            score = random.uniform(0.4, 0.6)
        else:
            nps = random.randint(0, 4)
            sentiment = 'negative'
            score = random.uniform(0.0, 0.3)
        
        responded_at = interaction['end_time'] + timedelta(hours=random.randint(1, 24))
        
        return {
            'id': None,
            'tenant_id': str(tenant_id),
            'interaction_id': interaction['id'],
            'survey_type': 'csat',
            'channel': 'in_app',
            'csat_score': csat,
            'nps_score': nps,
            'feedback_text': self._generate_feedback(csat),
            'sentiment': sentiment,
            'sentiment_score': round(score, 2),
            'survey_sent_at': interaction['end_time'] + timedelta(hours=1),
            'responded_at': responded_at,
            'created_at': responded_at,
            'updated_at': responded_at
        }
    
    @staticmethod
    def _generate_feedback(csat: int) -> str:
        """Generate realistic feedback text based on CSAT score"""
        if csat >= 4:
            return random.choice([
                "Çok memnun kaldım, teşekkürler!",
                "Harika bir hizmet, kesinlikle tavsiye ederim.",
                "Her şey mükemmeldi, çok teşekkürler."
            ])
        elif csat == 3:
            return random.choice([
                "İdare eder, beklentilerime uygundu.",
                "Ortalama bir deneyimdi.",
                "Normal, özel bir şey yoktu."
            ])
        else:
            return random.choice([
                "Pek memnun kalmadım, iyileştirme gerekiyor.",
                "Beklentimin altındaydı.",
                "Hayal kırıklığı yarattı."
            ])
