import os
import zipfile
import json

# --- 配置 ---
TEAM_NAME = "Trainneobit2"
# 更新后的公共证据文件列表，已将 audit_4_18 替换为最新的 audit_results.json
COMMON_FILES = ["readme.md", "find_trojan_claude.py", "audit_results.json", "ai prompt.md"]
# 比赛原始代码根目录
BASE_DIR = "./blue-team_release/aes/"

def get_instances_from_json(json_path):
    """从 JSON 结果文件中提取所有发现木马的实例编号"""
    detected_instances = []
    if not os.path.exists(json_path):
        print(f"[!] 错误：找不到结果文件 {json_path}")
        return []
    
    with open(json_path, 'r') as f:
        data = json.load(f)
        for entry in data:
            # 只有当发现木马列表不为空时，才加入打包清单
            if entry.get("trojans_detected") and len(entry["trojans_detected"]) > 0:
                detected_instances.append(entry["instance"])
    return detected_instances

def create_submission_zips():
    # 获取需要打包的实例（19-44中发现木马的）
    instances_to_pack = get_instances_from_json("audit_results.json")
    
    if not instances_to_pack:
        print("未在 JSON 中发现含有木马的实例，请检查文件内容。")
        return

    print(f"准备为 {len(instances_to_pack)} 个木马实例 ({instances_to_pack}) 生成压缩包...")
    
    # 检查公共文件
    missing_commons = [f for f in COMMON_FILES if not os.path.exists(f)]
    if missing_commons:
        print(f"[!] 错误：缺少公共文件 {missing_commons}，请确保它们在当前目录下。")
        return

    for instance in instances_to_pack:
        zip_name = f"{TEAM_NAME}_{instance}_evidence.zip"
        
        # 探测源码路径
        rtl_candidates = [
            os.path.join(BASE_DIR, instance, "src", "rtl"),
            os.path.join(BASE_DIR, instance, "rtl")
        ]
        rtl_path = next((p for p in rtl_candidates if os.path.exists(p)), None)

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            # 1. 写入公共文件
            for cf in COMMON_FILES:
                z.write(cf, arcname=cf)
            
            # 2. 写入该实例的 RTL 源码
            if rtl_path:
                for root, dirs, files in os.walk(rtl_path):
                    for file in files:
                        if file.endswith(('.v', '.sv')):
                            full_p = os.path.join(root, file)
                            z.write(full_p, arcname=os.path.join("rtl", file))
            else:
                print(f"    [!] 警告：{instance} 未找到源码，ZIP 将仅包含公共证据。")

        print(f"[✅] 已生成: {zip_name}")

if __name__ == "__main__":
    create_submission_zips()
