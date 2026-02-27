class ParticlePool:
    def __init__(self, max_particles=512):
        self.max = max_particles
        self.items = []

    def emit(self, x, y, vx, vy, ttl, color):
        if len(self.items) >= self.max:
            return
        self.items.append({'x':x,'y':y,'vx':vx,'vy':vy,'ttl':ttl,'c':color})

    def update(self, dt):
        alive=[]
        for p in self.items:
            p['x']+=p['vx']*dt; p['y']+=p['vy']*dt; p['ttl']-=dt
            if p['ttl']>0: alive.append(p)
        self.items=alive
