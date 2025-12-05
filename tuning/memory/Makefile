
# w = 2* CPU + 1
# --max-requests 1000 (vagy 2000) → worker újraindul számú kérés után (az arena lomtár ürül).
# --max-requests-jitter 50 → a restart időzítések ne legyenek szinkronban.
# --timeout 60 → ha worker lebénul, gunicorn újraindítja.

start-guvi:
	gunicorn \
		-k uvicorn.workers.UvicornWorker \
		-w 4 \
		--worker-connections 1000 \
		--timeout 60 \
		--max-requests 1200 \
		--max-requests-jitter 200 \
		myapp:app