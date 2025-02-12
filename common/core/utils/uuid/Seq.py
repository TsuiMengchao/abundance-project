import time
import math


class Seq:
    comm_seq_type = "COMMON"
    upload_seq_type = "UPLOAD"
    comm_seq = 1
    upload_seq = 1
    machine_code = "A"

    @staticmethod
    def getId(type=comm_seq_type, length=3):
        """
        核心的生成序列号的方法，对应Java版本中带AtomicInteger和int类型参数的getId方法
        """
        if type == Seq.upload_seq_type:
            atomic_int = Seq.upload_seq
        else:
            atomic_int = Seq.comm_seq
        result = time.strftime('%y%m%d%H%M%S', time.localtime())
        result += Seq.machine_code
        result += Seq.getSeq(atomic_int, length)
        return result

    @staticmethod
    def getSeq(atomic_int, length):
        """
        生成序列循环递增字符串，对应Java版本中的getSeq方法
        """
        # 先取值再+1，这里简单模拟原子操作，实际复杂场景可考虑使用线程安全相关机制完善
        value = atomic_int
        atomic_int = (atomic_int + 1) % (10 ** length)

        # 转字符串，用0左补齐
        return str(value).zfill(length)


if __name__ == "__main__":
    # 重新测试getId方法（无参数版本）
    common_seq_result = Seq.getId()
    print(f"无参数getId方法生成的通用序列号: {common_seq_result}")

    # 测试getId方法（带类型参数版本）
    common_type_seq_result = Seq.getId(Seq.comm_seq_type)
    print(f"带通用类型参数的getId方法生成的序列号: {common_type_seq_result}")
    upload_type_seq_result = Seq.getId(Seq.upload_seq_type)
    print(f"带上传类型参数的getId方法生成的序列号: {upload_type_seq_result}")

    # 测试getId方法（带自定义序列数和长度参数版本）
    custom_atomic_int = 1
    custom_length = 4
    custom_seq_result = Seq.getId(custom_atomic_int, custom_length)
    print(f"带自定义参数的getId方法生成的序列号: {custom_seq_result}")

    # 测试getSeq方法
    seq_value_result = Seq.getSeq(1, 3)
    print(f"getSeq方法生成的序列值: {seq_value_result}")