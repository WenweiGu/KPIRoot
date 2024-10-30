import pandas as pd
import time


class Align(object):
    @staticmethod
    def convert_time_to_str(timestamp) -> str:
        """
         时间格式化
        :param timestamp: 时间戳
        :return: %Y-%m-%d %H:%M:%S
        """
        if isinstance(timestamp, str):
            return timestamp
        time_local = time.localtime(int(timestamp))
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    @staticmethod
    def convert_time_to_timestamp(temp):
        """
        时间格式转换成时间戳
        """
        FMT = "%Y-%m-%d %H:%M:%S"
        timestamp = time.mktime(time.strptime(temp, FMT))
        return timestamp

    @staticmethod
    def convert_time_ms_to_s(timestamp):
        return int(int(timestamp) / 1000)

    @staticmethod
    def convert_time_s_to_ms(timestamp):
        return int(int(timestamp) * 1000)

    @staticmethod
    def timestamp_replace_seconds(df: pd.DataFrame) -> pd.DataFrame:
        df['time_index'] = pd.to_datetime(df['time_index'])
        df['time_index'] = df['time_index'].apply(lambda x: x.replace(second=0))
        return df

    def realign_online(self, target: pd.DataFrame, suspect: pd.DataFrame):
        # 时间戳只取到min
        time_col = 'time_index'
        suspect[time_col] = suspect[time_col].apply(lambda x: self.convert_time_ms_to_s(x))
        target[time_col] = target[time_col].apply(lambda x: self.convert_time_ms_to_s(x))
        suspect[time_col] = suspect[time_col].apply(
            lambda x: self.convert_time_to_str(x))
        suspect = self.timestamp_replace_seconds(suspect)
        target[time_col] = target[time_col].apply(
            lambda x: self.convert_time_to_str(x))
        target = self.timestamp_replace_seconds(target)
        df_all = pd.merge(target, suspect, how='outer', on=time_col)
        if not df_all.empty:
            df_all.set_index(time_col, inplace=True)
        df_all = df_all.dropna()
        return df_all
