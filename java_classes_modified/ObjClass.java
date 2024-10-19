@Entity
@Table(name="obj")
public class Obj implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long objId;

    @Column(name="user_id")
    private long userId;

    @Column(name="content")
    private String content;

    @Column(name="caso")
    private String caso;

    @OneToOne
    @JoinColumn(name="user")
    private User user;

}

