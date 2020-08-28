import grpc


import block_pb2
import block_pb2_grpc

def get_latest_block(stub):
  print block_pb2.OptionalBlock()
  block = stub.GetLatestBlock(block_pb2.OptionalBlock())
  return block

def run():
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = block_pb2_grpc.BlockFetcherStub(channel)
    print get_latest_block(stub)

if __name__ == '__main__':
  run()