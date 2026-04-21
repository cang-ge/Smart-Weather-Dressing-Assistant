#!/bin/bash
# 天气穿搭助手启动器

cd "$(dirname "$0")"

echo "=================================================="
echo "* Weather Outfit Assistant *"
echo "=================================================="
echo ""

# 默认城市
CITY=${1:-"Shanghai"}

echo "正在查询 $CITY 的天气信息..."
echo ""

python weather_agent.py << EOF
$CITY
EOF
