"""
Quick seed script: adds sample appointment/message interactions using the REAL Interaction schema.
Real schema has: id, tenant_id, title, description, type, start_time, end_time,
                 client_name, client_email, status, meta_data, created_at
Run: docker exec nextgent_backend python seed_messages.py
"""
import asyncio
import asyncpg
import uuid
import json
from datetime import datetime, timedelta


async def seed():
    conn = await asyncpg.connect(
        host='db', port=5432, user='postgres',
        password='postgres', database='nextgent'
    )
    tenants = await conn.fetch('SELECT id, name FROM tenants LIMIT 10')
    print(f'Tenants found: {len(tenants)}')

    samples = [
        ('whatsapp', 'Randevu Talebi', 'Merhaba, yakın zamanda bir randevu almak istiyorum.', 'Ayşe Kaya',  'ayse@example.com', 'inbound', 'unread'),
        ('email',    'Bilgi Talebi',   'Hizmetleriniz hakkında detaylı bilgi alabilir miyim?', 'Mehmet Demir','mehmet@example.com','inbound','read'),
        ('sms',      'Randevu Değişikliği','Yarınki randevuyu erteleyebilir miyiz?','Fatma Şahin','fatma@example.com','inbound','replied'),
        ('whatsapp', 'Teşekkür',        'Çok memnun kaldım, teşekkürler!', 'Ali Yıldız', 'ali@example.com','inbound','read'),
        ('email',    'Şikayet',         'Geçen haftaki hizmet ile ilgili bir sorunum var.','Zeynep Çelik','zeynep@example.com','inbound','read'),
        ('sms',      'Onay',            'Randevumu onaylıyorum.','Hasan Öztürk','hasan@example.com','inbound','read'),
        ('whatsapp', 'Kampanya Sorusu','Mevcut kampanyalarınız hakkında bilgi verir misiniz?','Leyla Arslan','leyla@example.com','inbound','unread'),
        ('email',    'Geri Bildirim',  'Sistemin çok kullanışlı olduğunu belirtmek istedim.','Emre Koç','emre@example.com','inbound','read'),
    ]

    total = 0
    for tenant in tenants:
        tid = tenant['id']
        for i, (itype, title, msg, cname, cemail, direction, status) in enumerate(samples):
            meta = json.dumps({'message': msg, 'direction': direction, 'status': status, 'customer_name': cname})
            start = datetime.utcnow() - timedelta(days=i, hours=i*2)
            end = start + timedelta(hours=1)
            await conn.execute(
                """
                INSERT INTO interactions
                    (id, tenant_id, type, title, description, start_time, end_time,
                     client_name, client_email, status, meta_data, created_at, updated_at, version)
                VALUES
                    ($1,$2,$3,$4,$5,$6,$7,$8,$9,'COMPLETED',$10::jsonb,$11,$11,1)
                ON CONFLICT DO NOTHING
                """,
                uuid.uuid4(), tid, itype, title, msg, start, end,
                cname, cemail, meta, start
            )
            total += 1
        print(f'  {tenant["name"]}: {len(samples)} interactions added')

    await conn.close()
    print(f'\nTotal records inserted: {total}')


if __name__ == '__main__':
    asyncio.run(seed())
