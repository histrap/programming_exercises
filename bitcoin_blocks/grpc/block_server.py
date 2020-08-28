from concurrent import futures
import grpc
import sqlite3

import block_pb2_grpc
import block_pb2

def get_db_conn(name='bitcoin'):
    conn = sqlite3.connect("%s.db" %(name))
    conn.row_factory = sqlite3.Row
    return conn

class BlockFetcherServicer(block_pb2_grpc.BlockFetcherServicer):
  def GetLatestBlock(self, request, context):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM blocks order by timestamp DESC limit 1")
    row = c.fetchone()
    if not row:
      return block_pb2.Block(hash='', timestamp='', block_index='', height='')

    block = block_pb2.Block(hash=row['hash'], timestamp=row['timestamp'], block_index=row['block_index'], height=row['height'])
    print block
    return block

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  block_pb2_grpc.add_BlockFetcherServicer_to_server(BlockFetcherServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
  serve()