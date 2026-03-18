from sklearn.utils.estimator_checks import check_estimator

from ktree import TreeCluster


for name, check in check_estimator(TreeCluster()):
    try:
        check(TreeCluster())
        print(f"✅ {name}")
    except Exception as e:
        print(f"❌ {name}: {e}")
