#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>
#include "birdisle.h"
#include "deps/hiredis/hiredis.h"

static void check(int result, const char *msg) {
    if (!result) {
        perror(msg);
        exit(1);
    }
}

#define COMMAND(ctx, ...) \
    do {                                                        \
        redisReply *reply = redisCommand(ctx, __VA_ARGS__);     \
        checkReply(ctx, reply, #__VA_ARGS__);                   \
    } while (0)

static void checkReply(redisContext *ctx, redisReply *reply, const char *cmd) {
    if (reply == NULL) {
        fprintf(stderr, "Command failed: %d\nCommand was %s\n",
                ctx->err, cmd);
        exit(1);
    } else if (reply->type == REDIS_REPLY_ERROR) {
        fprintf(stderr, "Command returned error: %s\nCommand was %s\n",
                reply->str, cmd);
        exit(1);
    } else {
        freeReplyObject(reply);
    }
}

static redisContext *connectBirdisle(birdisleServer *handle) {
    int sv[2];
    redisContext *ctx;

    check(socketpair(AF_UNIX, SOCK_STREAM, 0, sv) == 0, "socketpair");
    birdisleAddConnection(handle, sv[0]);
    ctx = redisConnectFd(sv[1]);
    check(ctx != NULL, "redisConnectFd");
    check(ctx->err == 0, "redisConnect");
    return ctx;
}

int main() {
    redisContext *ctx, *sub_ctx;
    redisReply *reply;

    birdisleServer *handle = birdisleStartServer("");
    ctx = connectBirdisle(handle);
    sub_ctx = connectBirdisle(handle);

    /* Simple type */
    COMMAND(ctx, "SET foo bar");
    /* List type */
    COMMAND(ctx, "RPUSH list value");
    /* Blocking commands (success and timeout) */
    COMMAND(ctx, "BRPOP list 0");
    COMMAND(ctx, "BRPOP list 1");
    /* Hash type */
    COMMAND(ctx, "HSET hfoo hbar hbaz");
    /* Stream type */
    COMMAND(ctx, "XADD mystream * sensor-id 1234 temperature 19.8");
    /* Miscellaneous */
    COMMAND(ctx, "INFO MEMORY");
    COMMAND(ctx, "DUMP foo");
    /* Scripts */
    COMMAND(ctx, "EVAL %s 2 0 %s", "return {redis.call('GET', KEYS[1])}", "foo");
    COMMAND(ctx, "SCRIPT LOAD %s", "return {redis.call('GET', KEYS[1])}");
    COMMAND(ctx, "EVALSHA %s 2 0 %s", "2ca09548f5032afef767c386656397a4db231a85", "foo");

    /* Pub-sub */
    COMMAND(sub_ctx, "SUBSCRIBE channel");
    COMMAND(ctx, "PUBLISH channel message");
    check(redisGetReply(sub_ctx, (void **) &reply) == REDIS_OK, "redisGetReply");
    checkReply(sub_ctx, reply, "<pubsub message>");

    /* Start a blocking command, then shut down the server before it completes */
    redisAppendCommand(ctx, "BRPOP list 0");

    birdisleStopServer(handle);
    redisFree(ctx);
}
