import asyncio
import httpx
import json
import sys
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

# Rich Console Setup (for beautiful output)
try:
    console = Console()
except:
    print("Lütfen 'rich' ve 'httpx' kütüphanelerini yükleyin: pip install rich httpx")
    sys.exit(1)

BASE_URL = "http://localhost:8000/api/v1"
HEALTH_URL = "http://localhost:8000/health"  # Or standard check

async def check_backend_health(client):
    """Backend sunucusunun ayakta olup olmadığını kontrol eder."""
    try:
        response = await client.get("http://localhost:8000/docs")
        if response.status_code == 200:
            return True, "✅ Backend Erişilebilir (Docs OK)"
        return False, f"❌ Backend Yanıt Vermiyor: {response.status_code}"
    except Exception as e:
        return False, f"❌ Bağlantı Hatası: {str(e)}"

async def test_pulse_endpoint(client):
    """Canlı veri akışını (Pulse Center) test eder."""
    try:
        response = await client.get(f"{BASE_URL}/analytics/pulse")
        if response.status_code == 200:
            data = response.json()
            table = Table(title="💎 Pulse Center (Canlı Veri)")
            table.add_column("Metrik", style="cyan")
            table.add_column("Değer", style="magenta")
            
            table.add_row("Aktif Çağrılar", str(data.get("activeCalls")))
            table.add_row("Dönüşüm Oranı", f"%{data.get("conversionRate")}")
            table.add_row("Bugünkü Müşteriler", str(data.get("todayClients")))
            table.add_row("Bekleyen Randevular", str(data.get("pendingAppointments")))
            
            console.print(table)
            return True
        else:
            console.print(f"[bold red]Pulse Hatası:[/bold red] {response.text}")
            return False
    except Exception as e:
        console.print(f"[bold red]Pulse Bağlantı Hatası:[/bold red] {e}")
        return False

async def test_chatbot(client):
    """Chatbot zekasını ve şirket bilgisini test eder."""
    questions = [
        "Fiyatlarınız nelerdir?",
        "Hangi sektörlere hizmet veriyorsunuz?"
    ]
    
    console.print(Panel("[bold yellow]🤖 Chatbot Zeka Testi Başlatılıyor...[/bold yellow]", expand=False))
    
    for q in questions:
        try:
            payload = {"message": q, "context": {"page": "test_script"}}
            start_time = time.time()
            response = await client.post(f"{BASE_URL}/helpdesk/chat", json=payload)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                ai_reply = data.get("response", "No response")
                
                console.print(f"\n[bold green]Soru:[/bold green] {q}")
                console.print(f"[bold blue]AI Yanıtı ({duration:.2f}s):[/bold blue] {ai_reply[:200]}...")
            else:
                console.print(f"[bold red]Chatbot Hatası:[/bold red] {response.status_code}")
        except Exception as e:
            console.print(f"[bold red]İstek Hatası:[/bold red] {e}")

async def simulate_vapi_call(client):
    """Vapi Webhook sistemini simüle eder."""
    payload = {
        "type": "call.ended",
        "call": {
            "id": "test-call-id-simulated",
            "startedAt": datetime.utcnow().isoformat() + "Z",
            "endedAt": datetime.utcnow().isoformat() + "Z",
            "customer": {"number": "+905551234567", "name": "Test Müşterisi"}
        },
        "transcript": "Merhaba, randevu almak istiyorum. Yarın saat 14:00 uygun mu?",
        "analysis": {"successEvaluation": "true", "summary": "Randevu talebi"}
    }
    
    console.print(Panel("[bold magenta]📞 Vapi Webhook Simülasyonu[/bold magenta]", expand=False))
    try:
        response = await client.post(f"{BASE_URL}/vapi/webhook", json=payload)
        if response.status_code == 200:
            console.print(f"✅ Webhook Başarıyla İletildi! [green]{response.json()}[/green]")
            console.print("[dim]Backend loglarında 'Test Müşterisi' ve şifrelenmiş veri kaydını kontrol edin.[/dim]")
            return True
        else:
            console.print(f"[bold red]Webhook Reddedildi:[/bold red] {response.status_code}")
            return False
    except Exception as e:
        console.print(f"[bold red]Webhook İletim Hatası:[/bold red] {e}")
        return False

async def main():
    console.print(Panel.fit("[bold white on blue] NextGent Sistem Tanı ve Analiz Aracı [/bold white on blue]", subtitle="v1.0"))
    
    async with httpx.AsyncClient() as client:
        # 1. Health Check
        with console.status("[bold green]Backend bağlantısı kontrol ediliyor...[/bold green]"):
            is_healthy, message = await check_backend_health(client)
            await asyncio.sleep(1)
        
        if is_healthy:
            console.print(message)
        else:
            console.print(message)
            console.print("[bold red]Lütfen backend sunucusunun (uvicorn) çalıştığından emin olun![/bold red]")
            return

        # 2. Pulse Test
        console.print("\n--- 📊 Veri Akış Analizi ---")
        await test_pulse_endpoint(client)
        
        # 3. Chatbot Test
        console.print("\n--- 🧠 AI Entegrasyon Analizi ---")
        await test_chatbot(client)

        # 4. Vapi Simulation
        console.print("\n--- ⚡ Webhook & Background Task Analizi ---")
        await simulate_vapi_call(client)
        
    console.print(Panel("[bold green]✅ Test ve Analiz Tamamlandı![/bold green]\nSistem stabil görünüyor. Manuel test için tarayıcıyı açabilirsiniz.", border_style="green"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
